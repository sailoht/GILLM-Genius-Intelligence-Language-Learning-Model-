from src.gillm.molecules.atom import DataAtom
from src.gillm.molecules.molecule import DataMolecule
from src.gillm.space.coordinates import SpatialCoordinate
from src.gillm.provenance.model import ProvenanceRecord
from src.gillm.core.enums import EpistemicStatus, ValidationStatus

def test_e_data_molecule():
    """
    Test E — information molecule:
    Create a Data Molecule with data, metadata, field, 3D position, relations, provenance, status.
    """
    atom = DataAtom(
        atom_id="atom_mass",
        atom_type="MASS",
        value=5.0,
        unit="kg"
    )
    prov = ProvenanceRecord(source_id="TestSensor", transformation_type="DIRECT_OBSERVATION")

    molecule = DataMolecule(
        molecule_id="mol_object_1",
        molecule_type="PHYSICAL_OBJECT",
        atoms={"mass": atom},
        state={"temperature": 298.15},
        spatial_position=SpatialCoordinate(x=10.0, y=5.0, z=0.0),
        provenance=prov,
        epistemic_status=EpistemicStatus.OBSERVED,
        validation_status=ValidationStatus.VALID
    )

    assert molecule.molecule_id == "mol_object_1"
    assert molecule.spatial_position.x == 10.0
    assert molecule.atoms["mass"].value == 5.0
    assert molecule.epistemic_status == EpistemicStatus.OBSERVED
