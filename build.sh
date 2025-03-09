pip install pyinstaller
# pyinstaller \
#     --onefile \
#     --windowed \
#     --icon="icon.ico" \
#     --distpath="./" \
#     --clean \
#     --specpath="./" \
#     --name="MyITS CR Rename" \
#     --upx-dir="./" \
#     main.py

pyinstaller --onefile --windowed --icon="icon.ico" --distpath="./" --clean --specpath="./" --name="MyITS CR Rename" --upx-dir="./" main.py