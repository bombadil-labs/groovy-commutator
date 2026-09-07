# Observed histories

## Definition

Let the full CA state evolve by \(S_{t+1}=E(S_t)\). An observation \(P\) and sampling stride \(q\) give \(U_k=P(S_{kq})\). A history of depth \(h\) includes the current observation and the preceding \(h\) observations.

In the current experiment, each time slice contributes a radius-one observed neighborhood. Depth six therefore contains 21 binary inputs. It is not a single-cell time series.

## Distinctions to preserve

Exact closure means the next observed state is determined by a specified observed neighborhood for every allowed fine state. Low prediction error is a finite-sample result for a fitted estimator. More history, a wider current neighborhood, and a different observation are separate changes to the prediction problem.
