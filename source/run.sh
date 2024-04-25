
if [ -f /mnt ];
then
module purge;
module load anaconda3;
else
alias python="python3.6m"
fi


export PYTHONPATH=$(pwd):$PYTHONPATH
python -c "
from DiskUsage import run; print(run); run('.local/du_config.yaml', './');
"