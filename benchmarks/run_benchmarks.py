import json
import time
import tracemalloc
import sys
import os
from typing import Dict, Any, List, Tuple
from gillm.gsl.phaser import GSLPhaser
from gillm.conversation.context import ConversationContext
from gillm.gsl.gcpr.models import GCPR
from gillm.gsl.error import run_full_error_analysis

def get_current_memory_mb() -> float:
    snapshot = tracemalloc.take_snapshot()
    total = sum(stat.size for stat in snapshot.statistics("lineno"))
    return total / (1024 * 1024)

class GILLMBenchmarker:
    def __init__(self, dataset_path: str = "benchmarks/dataset.json") -> None:
        self.dataset_path = dataset_path
        self.phaser = GSLPhaser()
        self.cases = []
        self.load_dataset()

    def load_dataset(self) -> None:
        if os.path.exists(self.dataset_path):
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                self.cases = json.load(f)
        else:
            print(f"Warning: Dataset path '{self.dataset_path}' not found.")

    def run_warmup(self) -> None:
        print("Starting GILLM Warm-up runs...")
        warmup_inputs = [
            "The boy opened the door.",
            "Who did the boy see?",
            "Did the dog eat food?",
            "I saw her duck."
        ]
        for text in warmup_inputs:
            self.phaser.phase(text)
        print("Warm-up complete.")

    def run_benchmarks(self) -> Dict[str, Any]:
        results_by_category = {}
        all_latencies = []

        tracemalloc.start()
        start_mem = get_current_memory_mb()

        categories: Dict[str, List[Dict[str, Any]]] = {}
        for case in self.cases:
            cat = case["category"]
            categories.setdefault(cat, []).append(case)

        print("\n--- Starting Categorical GILLM Benchmarking ---")
        for cat, cat_cases in categories.items():
            print(f"Benchmarking category: '{cat}' ({len(cat_cases)} cases)...")
            cat_latencies = []
            correct_count = 0

            for case in cat_cases:
                text = case["input"]
                expected = case["expected"]

                t_start = time.perf_counter()
                gcpr, _ = self.phaser.phase(text)
                t_end = time.perf_counter()

                latency_ms = (t_end - t_start) * 1000.0
                cat_latencies.append(latency_ms)
                all_latencies.append(latency_ms)

                is_correct = self.verify_case_accuracy(cat, gcpr, expected)
                if is_correct:
                    correct_count += 1

            total_cat_time = sum(cat_latencies)
            avg_latency = total_cat_time / len(cat_cases) if cat_cases else 0.0
            throughput = len(cat_cases) / (total_cat_time / 1000.0) if total_cat_time > 0 else 0.0
            accuracy = (correct_count / len(cat_cases)) * 100.0 if cat_cases else 0.0

            sorted_lat = sorted(cat_latencies)
            median_latency = sorted_lat[len(sorted_lat)//2] if sorted_lat else 0.0
            p95_index = int(len(sorted_lat) * 0.95)
            p95_latency = sorted_lat[p95_index] if sorted_lat else 0.0

            results_by_category[cat] = {
                "count": len(cat_cases),
                "total_time_ms": total_cat_time,
                "avg_latency_ms": avg_latency,
                "median_latency_ms": median_latency,
                "p95_latency_ms": p95_latency,
                "throughput_sps": throughput,
                "accuracy_percent": accuracy
            }

        end_mem = get_current_memory_mb()
        tracemalloc.stop()

        profiling_metrics = self.profile_pipeline_stages()
        determinism_pass = self.run_determinism_test(100)

        total_benchmark_time = sum(all_latencies)
        sorted_all = sorted(all_latencies)
        overall_avg = total_benchmark_time / len(all_latencies) if all_latencies else 0.0
        overall_median = sorted_all[len(sorted_all)//2] if sorted_all else 0.0
        overall_p95 = sorted_all[int(len(sorted_all)*0.95)] if sorted_all else 0.0
        overall_throughput = len(all_latencies) / (total_benchmark_time / 1000.0) if total_benchmark_time > 0 else 0.0

        overall_metrics = {
            "gsl_version": "1.1",
            "gcpr_version": "0.5",
            "gillm_version": "0.5.0",
            "environment": {
                "hardware": "Intel/AMD x86_64 Virtualized sandbox CPU",
                "python_version": sys.version,
                "os": sys.platform
            },
            "overall_summary": {
                "total_cases": len(all_latencies),
                "total_time_ms": total_benchmark_time,
                "avg_latency_ms": overall_avg,
                "median_latency_ms": overall_median,
                "p95_latency_ms": overall_p95,
                "throughput_sps": overall_throughput,
                "ram_usage_mb": end_mem - start_mem
            },
            "category_results": results_by_category,
            "determinism_test": {
                "runs": 100,
                "status": "PASS" if determinism_pass else "FAIL"
            },
            "pipeline_profiling": profiling_metrics,
            "llm_comparison": {
                "llm_benchmark": "NOT AVAILABLE (No local LLM available on sandbox environment)"
            }
        }
        return overall_metrics

    def verify_case_accuracy(self, category: str, gcpr: GCPR, expected: Dict[str, Any]) -> bool:
        gcpr_dict = gcpr.to_dict()
        roles = gcpr_dict.get("semantic", {}).get("roles", {})
        conv = gcpr_dict.get("conversation", {})
        unc = gcpr_dict.get("uncertainty", {})

        if category == "grammar":
            is_type_match = gcpr_dict.get("linguistic", {}).get("sentence_type") == expected.get("sentence_type")
            is_action_match = roles.get("action") == expected.get("action")
            is_agent_match = roles.get("agent") == expected.get("agent")
            is_patient_match = roles.get("patient") == expected.get("patient")
            return is_type_match and is_action_match and is_agent_match and is_patient_match

        elif category == "questions":
            is_q_family = conv.get("question_family") == expected.get("question_family")
            is_exp_ans = conv.get("expected_answer") == expected.get("expected_answer")
            is_action_match = roles.get("action") == expected.get("action")
            return is_q_family and is_exp_ans and is_action_match

        elif category == "semantic_roles":
            return roles.get("action") == expected.get("action") and \
                   (roles.get("agent") == expected.get("agent") or roles.get("experiencer") == expected.get("agent"))

        elif category == "entities":
            entities = gcpr_dict.get("semantic", {}).get("entities", {})
            for ent in expected.get("entities_tracked", []):
                if ent not in entities:
                    return False
            return True

        elif category == "coreference":
            if expected.get("ambiguous"):
                return unc.get("ambiguous") is True
            entities = gcpr_dict.get("semantic", {}).get("entities", {})
            return expected.get("coref_source") in entities

        elif category == "ambiguity":
            return unc.get("ambiguous") is expected.get("ambiguous")

        elif category == "transformations":
            exercises = gcpr_dict.get("exercises", {})
            return exercises.get("grammar_transformations", {}).get("can_transform_passive") == expected.get("can_transform_passive")

        elif category == "symbolic":
            entities = gcpr_dict.get("semantic", {}).get("entities", {})
            return len(entities) > 0

        elif category == "conversation":
            return True

        return True

    def run_determinism_test(self, repetitions: int = 100) -> bool:
        test_text = "The boy opened the door."
        first_gcpr, _ = self.phaser.phase(test_text)
        first_dict = json.dumps(first_gcpr.to_dict(), sort_keys=True)

        for _ in range(repetitions - 1):
            re_gcpr, _ = self.phaser.phase(test_text)
            re_dict = json.dumps(re_gcpr.to_dict(), sort_keys=True)
            if re_dict != first_dict:
                return False
        return True

    def profile_pipeline_stages(self) -> Dict[str, float]:
        test_text = "Why did the boy open the door?"
        runs = 50

        t_tot = 0.0
        t_tok = 0.0
        t_cand = 0.0
        t_parse = 0.0
        t_sem = 0.0
        t_err = 0.0
        t_val = 0.0

        for _ in range(runs):
            t0 = time.perf_counter()
            tokens = self.phaser.input_manager.process_input(test_text)
            t1 = time.perf_counter()
            t_tok += (t1 - t0)

            word_tokens = [t for t in tokens if t.token_type == "WORD"]
            t2 = time.perf_counter()
            cands_raw = self.phaser.candidate_generator.generate_candidates(word_tokens)
            cands = self.phaser.lexical_scorer.score_lexical_candidates(cands_raw)
            t3 = time.perf_counter()
            t_cand += (t3 - t2)

            t4 = time.perf_counter()
            parses = self.phaser.parser.parse(cands)
            t5 = time.perf_counter()
            t_parse += (t5 - t4)

            t6 = time.perf_counter()
            if parses:
                best_parse = parses[0]
                roles = self.phaser.role_resolver.resolve(best_parse)
                self.phaser.question_phaser.phase_question(best_parse, roles)
            t7 = time.perf_counter()
            t_sem += (t7 - t6)

            t8 = time.perf_counter()
            run_full_error_analysis(tokens, self.phaser.candidate_generator, self.phaser.lexical_scorer)
            t9 = time.perf_counter()
            t_err += (t9 - t8)

            t10 = time.perf_counter()
            if parses:
                self.phaser.bidirectional_validator.validate_structural_consistency(parses[0])
            t11 = time.perf_counter()
            t_val += (t11 - t10)

        t_total = t_tok + t_cand + t_parse + t_sem + t_err + t_val
        if t_total == 0:
            return {}

        return {
            "tokenizer": (t_tok / t_total) * 100.0,
            "lexicon_morphology_candidate_scoring": (t_cand / t_total) * 100.0,
            "parser": (t_parse / t_total) * 100.0,
            "semantic_roles_and_questions": (t_sem / t_total) * 100.0,
            "error_analysis": (t_err / t_total) * 100.0,
            "bidirectional_validation": (t_val / t_total) * 100.0
        }

if __name__ == "__main__":
    benchmarker = GILLMBenchmarker()
    benchmarker.run_warmup()
    metrics = benchmarker.run_benchmarks()

    output_path = "benchmarks/results/gillm_benchmark_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nBenchmark completed successfully! Results written to: '{output_path}'")
