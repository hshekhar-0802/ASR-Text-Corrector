# Correction Agent for ASR Errors in Voice-Enabled Assistants
## Introduction
Voice-enabled assistants (e.g., Alexa, Google Home or other voice triggered applications such as
search on a phone) rely on automatic speech recognition (ASR) to understand and respond to
spoken commands by a person. ASR systems convert audio received from a human speaking to
the device to the corresponding text for further processing. However, ASR systems can make
mistakes that lead to errors in the output text extracted from the input audio. These errors can
cause the assistant to misunderstand commands and potentially perform the wrong actions.
In this project, we consider two main types of errors:
- Similar-sounding characters may be incorrectly recognised. For example, “The boy is
eating” is recognized as “The eoy is eating” as the characters 'b' and 'e' can be mixed up.
- Whole words at the beginning or end of a sentence might be missing, where the speaker's
voice might be softer. For example, "I am going to the store” is recognised as “am going to
the store”.
## Resources
To correct these errors, the agent uses two key resources:
- <b>phoneme_table.json</b> : This file contains information on which characters might be
incorrectly recognised as others, providing possible substitutions that can occur.
- <b>vocabulary.json</b> : This file lists the possible missing words that could appear at the start or
end of the text received.
## Cost Model
This is implemented using OpenAI Whisper model. Whisper is an ASR model that computes the likelihood of a text s for a given
audio a. Specifically, it breaks down the text into sequences of tokens text [t<sub>1</sub>, t<sub>2</sub>,...., t<sub>n</sub>]
where each token t<sub>i</sub> consists of one or more characters. Then, Whisper computes the negative log likelihood as: <br>
$$\boxed{L(s, a) = -\log(P_{\theta}(s|a)) = -\sum_{i=1}^n \log(P_{\theta}(t_i|t_1,t_2,\ldots,t_{i-1}, a))}$$<br>
Here, θ
denotes the parameters of the Whisper model which obtained by large-scale training. In
essence, the Whisper model provides a cost function or a coherence score that relates the audio
received with candidate text that your algorithm may consider. Formally, we the cost of a text
s
as for a given audio a is expressed as f<sub>cost</sub>(s)=L(s,a).
## Input Details
The agent requires three files as input:
- <b>data.pkl</b> : This is the main input file which consists of the sound data and the text returned by Voice Assistant. It is a pickled list of dictionaries. Each dictionary has two keys: <i>'audio'</i> and <i>'text'</i>. dict['audio'] is another dictionary with two keys: <i>'array'</i> and <i>'sampling rate'</i>. dict['text'] contains the text returned by the Voice Assistant.
- <b>vocabulary.json</b>
- <b>phoneme_table.json</b>
## Execution
- ### Creating Environment
  You can create a conda environment using the ```environment.yml``` file provided.<br>
  ```conda env create -f environment.yml```
- ### Running the code
  Create the 3 input files and place them in the ```data``` directory, and simply run the following command: <br>
  ```python driver.py --output_file=output.json```
  Alternatively,
  ```python driver.py --input_file=<path_to_data.pkl> --phoneme_file=<path_to_phoneme_table.json> --vocab_file=<path_to_vocabulary.json> --output_file=output.json```

## Tests
[![Play audio]([https://www.example.com/audio_button_image.png](https://img.freepik.com/premium-vector/play-pause-icon-set-music-audio-video-start-pause-button-vector-symbol-black-filled-outlined-style_268104-12801.jpg?w=1380))]([https://www.example.com/path_to_audio_file.mp3](https://www2.cs.uic.edu/~i101/SoundFiles/StarWars3.wav))
