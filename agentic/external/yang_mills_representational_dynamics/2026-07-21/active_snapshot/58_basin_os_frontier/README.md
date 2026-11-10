# Stage 58 -- basin and OS frontier

This stage composes the five-target run, supplies the temporal countermodel,
and audits the exact boundary between the new finite theorems and physical
Yang--Mills.

The theorem note is `basin_os_frontier_theorem.pdf`.

```bash
python3 basin_os_frontier.py --write basin_os_frontier_results.json
python3 -m unittest -v test_basin_os_frontier.py
```
