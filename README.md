# Optimal_Fantasy_Smash
## Instructions
1. Clone this repo
  
  ```
  git clone https://github.com/ekuecks/Optimal_Fantasy_Smash.git
  ```

2. Edit the data/players.txt file with the results of the tournament with the format
  ```
  roster_spots salary_cap
  place name salary score
  place name salary score
  ...
  ```
  See the sample file for Genesis 3
  
3. run `python3 optimal.py` to see the optimal lineup for that tournament
  
  Alternatively, put your results in any file and run `python3 optimal.py --filename <filename>` e.g. `python3 optimal.py --filename data/sm4sh_example.txt`
