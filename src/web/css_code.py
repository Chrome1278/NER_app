file_uploader_css = '''
<style>
[data-testid="stFileUploadDropzone"] div div::before {
    color:black; 
    content:"Для загрузки файла перетяните его сюда или просто нажмите на поле"
}
[data-testid="stFileUploadDropzone"] div div span {display:none;}
[data-testid="stFileUploadDropzone"] div div::after {
    color:#555;
    font-size: .9em;
    content:"Максимальный размер файла: 200MB, Форматы: CSV, TXT"
 }
[data-testid="stFileUploadDropzone"] div div small {display:none;}

.edgvbvh9 {display:none;}

</style>
'''