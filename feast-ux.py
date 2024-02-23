import os, subprocess
subprocess.run("cd ~/feast_project/feature_repo; feast ui   --host localhost --port $CDSW_APP_PORT",shell=True, env=dict(os.environ))
