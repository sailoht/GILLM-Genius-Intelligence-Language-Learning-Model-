from gillm.gsl.gcpr.models import GCPR, SurfaceRepresentation
from gillm.gsl.gcpr.validator import GCPRValidator

def test_gcpr_validation():
    surface = SurfaceRepresentation(original_text="Test sentence", tokens=[])
    gcpr_obj = GCPR(surface=surface)

    # Convert to dict
    data = gcpr_obj.to_dict()

    # Validate
    is_valid, errors = GCPRValidator.validate(data)
    assert is_valid, f"Validation failed with: {errors}"
