---
layout: post
title: "It's Coming...Rome"
author: 'Victor Kristof and Lucas Maystre'
---

_Forza Italia!_
We first wanted to congratulate the Italian team for an amazing Euro.
They displayed some very attractive football and contributed to a competition with lots of emotions.
They have also beaten the Kickoff.ai's odds, as our _Kickscore_ model [gave a higher probability of winning to England][final]: Italy had 30% chances to win, and England 39%.
But does it mean we made a mistake?

## How accurate are your predictions?

One question we're often asked is "how accurate are your predictions?".
Our answer is usually unsatisfactory, because our model, by design, makes errors.
In fact, no predictive models of football matches, Kickscore included, will ever predict a win for [Czech Republic against the Netherlands][czechrepulic-netherlands], even though this was the outcome.
Football is a sport with a [high level of randomness][wunderlich2021influence], in which one expects the unexpected!
Yet, as shown in the plot below, Kickscore reaches an accuracy of 56.9%.
This is (fortunately) better than if we were predicting all matches at random, in which case our performance would be 33%.
We can also compute the accuracy obtained by the betting odds of some of the main bookmakers, which reaches 54.9%.
Hence, although the accuracy of our model is much better than a random predictor and a bit better than that of the betting odds, it is still far for 100%.

![Accuracy obtained by Kickoff.ai and some of the major bookmakers.](/assets/posts/eu20-analysis/accuracy.png)
_Accuracy obtained by Kickoff.ai and some of the major bookmakers. Higher is better._

## All models are wrong, but some are useful

Predicting the outcome of a match is a difficult task - and one that is perhaps not the most useful and interesting.
Football is a game of skill and luck, influenced by many factors and in which a part of randomness is always present.
To take this uncertainty into account, statistical modelers and sports analysts design models that predict the _probabilities_ of each outcome.
A **probabilistic** model enables a more fine-grained analysis than a model that only predicts the outcome of a match (which is called a _deterministic_ model), and provides a measure of how expected (or not) an outcome was.
For example, probabilistic models, such as Kickscore, can be used for [scouting new talents][scouting], for [enriching media articles][media], for [detecting fraud][fraud], and for [setting betting odds][odds].

However, even though probabilistic models provide many benefits, their major drawback lies in how to evaluate their predictions.
The straightforward approach is to pick the outcome with the highest probability and decide that this is the model's prediction.
This is actually what we have done above to compute the accuracy.
But, doing so, we lose the crucial information contained in the probabilities, throwing the baby out with with the bathwater!

Instead, to keep the probabilities intact, we must use other metrics, such as the [Brier score][brier] and the [logarithmic loss][logloss] (referred to as the "log loss").
These metrics can be understood as penalizing predictions that are both confident and wrong.
But interpreting them in absolute terms are difficult, and we have to _compare_ the performance scores of several models in order to determine which one is the best.
This is what we have done in our analysis of the [World Cup 2018][previous-blog], where we compared Kickscore against the predictions of Google, FiveThirtyEight, and the bookmakers.
For the Euro 2020, unfortunately, we can compare our performance only to that of the bookmakers, because Google and FiveThirtyEight didn't provide predictions for this competition.

We choose to use the log loss to evaluate our performance (for reasons that our out of the scope of this blog post).
The log loss is a value contained between 0 (highly confident and correct prediction) and infinity (highly confident and wrong prediction).
Hence, a **lower** value is better.
We show in the following figure the log loss for our model and for all bookmakers in our database.
A random predictor that assigns a 33.33% probability to each outcome of each match reaches a log loss of 1.0986.
Kickoff.ai's model obtains 0.9650, and the best log loss among the bookmakers is obtained by William Hill with 0.9829.

![Log loss obtained by Kickoff.ai and some of the major bookmakers.](/assets/posts/eu20-analysis/logloss.png)
_Log loss obtained by Kickoff.ai and some of the major bookmakers. Lower is better._

## We (fortunately don't) live in a simulation

Another way of evaluating our model is by simulating the whole tournament and compare our most likely winners to that of other models.

- This year, [Goldman Sachs has provided such predictions][goldman-sachs-report]: they predicted the Euro 2020 winner to be Belgium (21.7%), Portugal (11.6%), England (10.9%), France (10.5%), or Spain (10.2%).
- They also provided the predictions of the winner obtained by the betting odds on Betfair: England (20%), France (16%), Belgium (13%), Spain (12.5%), or Germany/Italy (11%).
- On our side, we obtain these predictions: England (17.1%), Italy (16.4%), Spain (12.1%), France (12%), and Belgium (9.4%)

[TODO: Show bar plot or table for winner prediction]

## Will I become rich using Kickoff.ai's predictions?

A third way of evaluating our predicted outcome probabilities is by playing against the betting odds and analyzing how much money we could have won (or lost...).

- To do so, we use the following strategy to play against 10 bookmakers:
- [TODO: Describe strategy.]

[TODO: Show plot of money won/lost during the Euro.]

[final]: http://kickoff.ai/match/72811
[czechrepulic-netherlands]: http://kickoff.ai/match/72799
[wunderlich2021influence]: https://www.tandfonline.com/doi/full/10.1080/02640414.2021.1930685
[previous-blog]: https://blog.kickoff.ai/2018-07-20/world-cup-2018-analysis
[goldman-sachs-report]: https://www.goldmansachs.com/insights/pages/gs-research/euro-2020/report.pdf
[scouting]: https://www.nbcnews.com/mach/science/how-ai-helping-sports-teams-scout-star-players-ncna882516
[media]: https://fivethirtyeight.com/sports/
[fraud]: https://core.ac.uk/download/pdf/266989334.pdf
[odds]: https://tradematesports.medium.com/how-bookmakers-create-their-odds-from-a-former-odds-compiler-5b36b4937439
[brier]: https://en.wikipedia.org/wiki/Brier_score
[logloss]: https://en.wikipedia.org/wiki/Cross_entropy
