async function ocrOutput(imageFile) {

    const formdata = new FormData()
    formdata.append('file', imageFile)

    try{
        console.log("BEFORE DATA")
        const response = await fetch("/ocr-to-latex", {
            method: "POST",
            body: formdata
        });
        console.log("AFTER DATA")

        const data = await response.text()
        console.log(data)
        const fixedLatex = data.replace(/\\\\/g, '\\');
        console.log(fixedLatex)
        console.log("DATA: ", fixedLatex)

        if(data){
            return fixedLatex;
        } else {
            return data.error || 'OCR failed';
        }
                
    } catch (error) {
        return "Error: " + error.message;
     }
}