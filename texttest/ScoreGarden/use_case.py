from step_definitions import *

select_garden_size("Balcony")
select_flowers(["daisy"])
submit_garden_quizz()
wait_for_garden_quizz_response()
