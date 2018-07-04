WORKDIR=${1:-"/home/DEV.T1.TBS-SCT.GC.CA/dsamojle-ps/"}
mkdir -p $WORKDIR
cd $WORKDIR
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
tar -czvf track-web.tar.gz .venv track
rm -rf .venv
