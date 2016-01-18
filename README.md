# Optimal_Fantasy_Smash
## Instructions
1. Clone this repo
  
  ```
  git clone https://github.com/ekuecks/Optimal_Fantasy_Smash.git
  ```

2. Edit the players.txt file with the results of the tournament with the format
  ```
  salary_cap
  place name salary score
  place name salary score
  ...
  ```
  See the sample file for Genesis 3 (top 8 currently projected)
  
3. run `python optimal.py` to see the optimal lineup for that tournament
  
  Alternatively, put your results in any file and run `python optimal.py filename` e.g. `python optimal.py sm4sh_example.txt`
