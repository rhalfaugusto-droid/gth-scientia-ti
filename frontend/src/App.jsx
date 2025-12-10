import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import CadastroEmpresa from './pages/CadastroEmpresa'
import CadastroTributario from './pages/CadastroTributario'
import Workspace from './pages/Workspace'
import Builder from './pages/Builder'
import Nav from './components/Nav'

export default function App(){
  return (
    <BrowserRouter>
      <Nav />
      <Routes>
        <Route path='/' element={<Login/>} />
        <Route path='/cadastro-empresa' element={<CadastroEmpresa/>} />
        <Route path='/cadastro-tributario' element={<CadastroTributario/>} />
        <Route path='/workspace' element={<Workspace/>} />
        <Route path='/builder' element={<Builder/>} />
      </Routes>
    </BrowserRouter>
  )
}
