async function ocrOutput(imageFile) {

    const formdata = new FormData()
    formdata.append('file', file)

    try{
        const response = await fetch("/ocr-to-latex", {
            method: "POST",
            body: formdata
        });

        const data = await response.text()
        if(data){
            return data;
        } else {
            return data.error || 'OCR failed';

        }
                
    } catch (error) {
        return "Error: " + error.message;
     }
}