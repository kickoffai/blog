---
layout: post
title: "It's Coming...Rome"
author: 'Victor Kristof and Lucas Maystre'
---

_Viva Italia!_
We first wanted to congratulate the Italian team for an amazing Euro.
They displayed some very attractive football and contributed to a competition with lots of emotions.
They have also beaten the Kickoff.ai's odds, as our model, that we call _Kickscore_, [gave a higher probability of winning to England][final]: Italy had 30% chances and England 39%.
But does it mean we made a mistake?

One question we're often asked is "how accurate are your predictions?".
Our answer is usually unsatisfactory, because our model, by design, makes some errors.
In fact, no predictive models of football matches, Kickscore included, will (can?) ever predict a win for [Czech Republic against the Netherlands][czechrepulic-netherlands], even though this was the outcome.
Football is a sport with a [high level of randomness][wunderlich2021influence], and the unexpected is expected!
Yet, as shown the plot below, Kickscore reaches an accuracy of XX%.
This (fortunately!) better than if we were predicting all matches at random, in which case our performance would be 33%.
We can also compare the accuracy obtained by the betting odds of some of the main bookmakers, which reaches XX%.

[TODO: Show plot of accuracy.]

Predicting the outcome of a match is hence a difficult task - and one that is perhaps not the most useful.
- Instead, it's more interesting and useful to predict the _probabilities_ of outcome, which is what our model does.
- It is more useful to understand if an outcome is more or less expected, according to a model, as it enables a more fine-grained analysis.
- Applications to scouting, media, fraud detection, and betting.
- Problem: this is usually more difficult to analyze the performance of such a model.

There exists different metrics to do so, such as the [Brier score] and the [logarithmic loss].
- One issue with such metrics is that the value they give is difficult to interpret in absolute terms.
- Rather, we have to *compare* the performance scores of several models in order to determine which one is the best.
- This is what we have done for the [WC2018][previous-blog], where we compare Kickscore against predictions by Google, FiveThirtyEight, and the bookmakers.
- For the Euro 2020, we can only compare against the bookmakers.

[TODO: Show plot of log-loss.]

Another way of evaluating our model is by simulating the whole tournament and compare our most likely winners to that of other models.
- This year, [Goldman Sachs has provided such predictions][goldman-sachs-report]: they predicted the Euro 2020 winner to be Belgium (21.7%), Portugal (11.6%), England (10.9%), France (10.5%), or Spain (10.2%).
- They also provided the predictions of the winner obtained by the betting odds on Betfair: England (20%), France (16%), Belgium (13%), Spain (12.5%), or Germany/Italy (11%).
- On our side, we obtain these predictions: England (17.1%), Italy (16.4%), Spain (12.1%), France (12%), and Belgium (9.4%)

[TODO: Show bar plot or table for winner prediction]

A third way of evaluating our predicted outcome probabilities is by playing against the betting odds and analyzing how much money we could have won (or lost...).
- To do so, we use the following strategy to play against 10 bookmakers:
- [TODO: Describe strategy.]

[TODO: Show plot of money won/lost during the Euro.]

[final]: http://kickoff.ai/match/72811
[czechrepulic-netherlands]: http://kickoff.ai/match/72799
[wunderlich2021influence]: https://www.tandfonline.com/doi/full/10.1080/02640414.2021.1930685
[previous-blog]: https://blog.kickoff.ai/2018-07-20/world-cup-2018-analysis
[goldman-sachs-report]: https://www.goldmansachs.com/insights/pages/gs-research/euro-2020/report.pdf
