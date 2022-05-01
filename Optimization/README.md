This program shows the topic of Optimization in the field of Artificial Intelligence. It uses the real-world problem of optimizing the different variables that can be changed on a toaster. In this case, these variables can be the time you toast the toast, the time you wait before eating the toast, the type of toaster, and the toaster's power.

-> optimizing_toast_easy
- implement it with only two parameters: toast_duration and wait_duration
- e.g., utility(2,3)
- Implement the function by testing all possible values for these variables.
- (This state space has only 10000 values, so it shouldn't take too long)


-> optimize_toast_medium
- same as easy, but implement hill climbing
- see pseudo code


-> optimize_toast_hard_v1 uses gradient ascent for parameters toast_duration wait_duration and power.
-> optimize_toast_hard_v2 uses gradient ascent just for parameter power and uses hill climbing for parameters toast_duration and wait_duration.
- also use the parameter power
- e.g., utility(2,3,1.2)
- this introduces the following complications:
  - multiple maxima
  - a continuous parameter
- implement gradient ascent


-> optimize_toast_very_hard_v1 uses gradient ascent for parameters toast_duration wait_duration and power.
-> optimize_toast_very_hard_v2 uses gradient ascent just for parameter power and uses hill climbing for parameters toast_duration and wait_duration.
- Same as hard, but use repeated search to find all maxima.
- repeated search:
  - apply gradient descent from different starting points.
- I think there are 5 maxima. But I'm not sure :-P


-> optimize_toast_prepare
- find the optimum for all four parameters
- define your own algorithm!
