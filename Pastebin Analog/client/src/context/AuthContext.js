import { createContext, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom'
import jwt_decode from 'jwt-decode'

const AuthContext = createContext()
export default AuthContext


export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(
    () => localStorage.getItem('authTokens')
      ? JSON.parse(localStorage.getItem('authTokens'))
      : null
  )

  const [user, setUser] = useState(
    () => localStorage.getItem('authTokens')
      ? jwt_decode(localStorage.getItem('authTokens'))
      : null
  )

  const [loading, setLoading] = useState()

  const loginUser = async (credentials) => {
    let response = await fetch('/api/v1/users/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
    let data = await response.json()

    if (response.status === 200) {
      setAuthTokens(data)
      setUser(jwt_decode(data.access))
      localStorage.setItem('authTokens', JSON.stringify(data))
    }
    return response.status
  }

  const registerUser = async (credentials) => {
    let response = await fetch('/api/v1/users/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })

    let data = await response.json()
    return {data: data, status: response.status}
  }

  const logoutUser = () => {
    setAuthTokens(null)
    setUser(null)
    localStorage.removeItem('authTokens')
  }

  const updateToken = async () => {
    let response = await fetch('/api/v1/token/refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'refresh': authTokens?.refresh})
    })

    let data = await response.json()

    if (response.status === 200){
      setAuthTokens(data)
      setUser(jwt_decode(data.access))
      localStorage.setItem('authTokens', JSON.stringify(data))
    }

    if (loading) {
      setLoading(false)
    }
  }

  let contextData = {
    user: user,
    authTokens: authTokens,
    logoutUser: logoutUser,
    loginUser: loginUser,
    registerUser: registerUser,
  }

  useEffect(() => {
    if (loading) {
      updateToken()
    }
    const fiveMinutes = 1000 * 60 * 5
    const interval = setInterval(() => {
      if (authTokens) {
        updateToken()
      }
    }, fiveMinutes)
    return () => clearInterval(interval)

  }, [authTokens, loading])

  return (
    <AuthContext.Provider value={contextData}>
      {loading ? null : children}
    </AuthContext.Provider>
  )
}