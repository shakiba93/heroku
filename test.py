import timeit

def test_speech():
	from api_functions import speech_recog
	speech_recog("SoftComputing-AbbasMohammadi.m4a.wav")

print(timeit.timeit('test_speech()', number=1,globals=globals()))
