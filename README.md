# part-of-speech-tagger
to run the program from the command line, run
  python main.py <opt>=<arg>

  where options: smoothing (args = LAP, NONE) - if no smoothing mentioned, Laplace will be used
                 trainstart (args - numerical) - which brown sentence to start from, default 0
                 trainlength (args- numerical) - how many sentences to train on, default 5000
