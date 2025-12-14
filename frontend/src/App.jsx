// frontend/src/App.jsx
import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import TaxSimulation from './pages/TaxSimulation'
import Login from './pages/Login'
import CadastroEmpresa from './pages/CadastroEmpresa'
import CadastroTributario from './pages/CadastroTributario'
import Builder from './pages/Builder'
import BuilderWorkflow from './pages/BuilderWorkflow'
import Nav from './components/Nav'
import { AnimatePresence } from 'framer-motion'
import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

export default function App(){
  return (
    <BrowserRouter>
      <Nav />
      <AnimatePresence mode='wait'>
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/cadastro-empresa' element={<CadastroEmpresa />} />
          <Route path='/cadastro-tributario' element={<CadastroTributario />} />
          <Route path='/workspace' element={<Dashboard />} />
          <Route path='/simulation' element={<TaxSimulation />} />

          {/* Builder page (drag & drop) */}
          <Route
            path='/builder'
            element={
              <DndProvider backend={HTML5Backend}>
                <Builder />
              </DndProvider>
            }
          />

          {/* Expanded full-screen workflow editor (new route) */}
          <Route path='/builder/workflow' element={<BuilderWorkflow />} />

          <Route path='*' element={<Navigate to='/' />} />
        </Routes>
      </AnimatePresence>
    </BrowserRouter>
  )
}
