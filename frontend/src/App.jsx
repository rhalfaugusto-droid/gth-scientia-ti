import React, {useState} from 'react'
import axios from 'axios'

export default function App(){
  const [file, setFile] = useState(null)
  const [text, setText] = useState('')
  const upload = async () => {
    if(!file) return alert('select file')
    const fd = new FormData()
    fd.append('file', file)
    const r = await axios.post('/docs/upload', fd, { headers: {'Content-Type':'multipart/form-data'} })
    setText(r.data.text || 'no text')
  }
  return (<div style={{padding:20,fontFamily:'Arial'}}>
    <h1>GTH - Upload OCR</h1>
    <input type="file" onChange={e=>setFile(e.target.files[0])} />
    <button onClick={upload}>Upload</button>
    <pre>{text}</pre>
  </div>)
}
