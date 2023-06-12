import { useState, useContext } from 'react'
import * as S from './LoginRegisterModal.styled'
import RightArrowImage from '../../assets/images/LoginRegisterModal/RightArrowImage.svg'
import CloseButtonImage from '../../assets/images/LoginRegisterModal/CloseButtonImage.svg'
import AuthContext from '../../context/AuthContext'


const LoginRegisterModal = ({ modalState, setModalState }) => {
  const {loginUser, registerUser} = useContext(AuthContext)
  const [loginCredentials, setLoginCredentials] = 
    useState({email: '', password: ''})
  const [registerCredentials, setRegisterCredentials] =
    useState({username: '', email: '', password: '', confirm_password: ''})
  const [errorCredentials, setErrorCredentials] = useState({})

  let modalContent = null
  let bottomButton = null
  
  const [loginValid, setLoginValid] = useState(true)

  const handleLoginEmailChange = (e) => {
    setLoginCredentials({...loginCredentials, email: e.target.value })
  }

  const handleLoginPasswordChange = (e) => {
    setLoginCredentials({ ...loginCredentials, password: e.target.value })
  }

  const handleLoginClick = () => {
    setLoginValid(true)
    loginUser(loginCredentials).then(
      status => {
        if (status === 200){
          setModalState('no modal')
        }
        else {
          setLoginValid(false)
        }
      }
    )
  }

  const handleRegisterUsernameChange = (e) => {
    setRegisterCredentials({ ...registerCredentials, username: e.target.value })
  }

  const handleRegisterEmailChange = (e) => {
    setRegisterCredentials({ ...registerCredentials, email: e.target.value })
  }

  const handleRegisterPasswordChange = (e) => {
    setRegisterCredentials({ ...registerCredentials, password: e.target.value })
  }

  const handleRegisterConfirmPasswordChange = (e) => {
    setRegisterCredentials({ ...registerCredentials, confirm_password: e.target.value })
  }

  const handleRegisterClick = () => {
    setErrorCredentials({})
    registerUser(registerCredentials).then(
      response_obj => {
        if (response_obj.status !== 201){
          setErrorCredentials(response_obj.data)
          
        }
      }
    )  
  }

  if (modalState === 'login'){
    modalContent = 
      <>
        <S.Title>Login</S.Title>
        <S.Input
          placeholder="Email..."
          onChange={handleLoginEmailChange}/>
        <S.Input
          placeholder="Password..." type="password"
          onChange={handleLoginPasswordChange}/>
        {!loginValid && <S.LoginErrorMessage>Incorrect email or password</S.LoginErrorMessage>}
        <S.LoginButton onClick={handleLoginClick}>
          Log in!
        </S.LoginButton>
      </>
    
    bottomButton =
      <S.ButtonWrapper>
        <S.ToRegisterButton onClick={() => setModalState('register')}>
          or register
          <S.RightArrow src={RightArrowImage}/>
        </S.ToRegisterButton>
      </S.ButtonWrapper>

  } else if (modalState === 'register'){
    modalContent =
    <>
      <S.Title>Register</S.Title>
      <S.Input
        placeholder="Username..."
        onChange={handleRegisterUsernameChange}
      />
      {errorCredentials.username && (
        <S.ErrorMessage>{errorCredentials.username[0]}</S.ErrorMessage>
      )}  
      <S.Input
        placeholder="Email..."
        onChange={handleRegisterEmailChange}
      />
      {errorCredentials.email && (
        <S.ErrorMessage>{errorCredentials.email[0]}</S.ErrorMessage>
      )}
      <S.Input
        placeholder="Password..." type='password'
        onChange={handleRegisterPasswordChange}
      />
      {errorCredentials.password && (
        <S.ErrorMessage>{errorCredentials.password[0]}</S.ErrorMessage>
      )}
      <S.Input
        placeholder="Confirm password..." type='password'
        onChange={handleRegisterConfirmPasswordChange}
      />
      {errorCredentials.confirm_password && (
        <S.ErrorMessage>{errorCredentials.confirm_password[0]}</S.ErrorMessage>
      )}
      <S.RegisterButton onClick={handleRegisterClick}>Sign up!</S.RegisterButton>
    </>

    bottomButton = 
      <S.ButtonWrapper>
        <S.ToLoginButton onClick={() => setModalState('login')}>
          or login
          <S.RightArrow src={RightArrowImage}/>
        </S.ToLoginButton>
      </S.ButtonWrapper>
  }
  return (
    <S.Container>
      <S.Modal>
        {modalContent}
        <S.CloseButton src={CloseButtonImage}
          onClick={() => setModalState('no modal')}/>
      </S.Modal>
      {bottomButton}
    </S.Container>
  )
}

export default LoginRegisterModal