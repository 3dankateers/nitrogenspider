# nitrogenspider

Purpose: <br>
  Hard code list of tournament names<br>
  for each tournament name:<br>
    use selenium to scrape https://nitrogensports.eu/sport/esports/tournament_name<br>
    parse bets available<br>
    for each possible bet, store in db:<br>
      Tournament identifier<br>
      Money line for each side(odds)<br>
      Team names for each side<br>
      date grabbed<br><br>
      
I don't think we care about historical odd changes so new money lines would overwrite old money lines.
Program should be scheduled every 5minutes? on a constantly running service.
