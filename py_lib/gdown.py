## cmd/ powershell 동작하는데, python terminal에서 run만 안 됨
import gdown

# url = 'https://drive.google.com/open?id=137RyRjvTBkBiIfeYBNZBtViDHQ6_Ewsp'
# 이거 안됨, param: export=download 줘야지 다운로드됨
url = 'https://drive.google.com/u/0/uc?id=137RyRjvTBkBiIfeYBNZBtViDHQ6_Ewsp&export=download'
output = '101_ObjectCategories.tar.gz'
gdown.download(url, output, quiet=False)