from django.test import TestCase
from .standard_image_extraction import standard_image
from .image_rotation import rotate_image
from .identify_Idname import rotation_check
import cv2


# standard image tests
good_image = cv2.imread("Muntaka.jpg")
input_value = rotate_image(good_image)
class StandardImageTestCase(TestCase):
        def test_standard_image(self):
                    self.assertEqual(
                                        {
                                                            "surname": "MUNTAKA",
                                                                            "firstname": "MOHAMMEDMUBARAK",
                                                                                            "sex": "M",
                                                                                                            "nationality": "Ghanaian",
                                                                                                                            "date_of_birth": "17/10/1971",
                                                                                                                                            "height": "1.80",
                                                                                                                                                            "id_number": "GHA-5335998802-1",
                                                                                                                                                                            "document_number": "GH1507126",
                                                                                                                                                                                            "place_of_birth": "ACCRA",
                                                                                                                                                                                                            "date_of_issuance": "13/06/2018",
                                                                                                                                                                                                                            "date_of_expiry": "11/06/2028"


                                                                                                                                                                                                                                        },
                                                    input_value
                                                                )
                            
                    # test rotation
                    tilted_image = cv2.imread("Muntaka90clockwise.jpg")
                    input_1 = rotation_check(good_image)
                    input_2 = rotation_check(tilted_image)
                    class RotationCheckTestCase(TestCase):
                            def test_rotation_check(self):
                                        self.assertEqual(True, input_1[0])
                                                self.assertEqual(False, input_2[0])



                                                
