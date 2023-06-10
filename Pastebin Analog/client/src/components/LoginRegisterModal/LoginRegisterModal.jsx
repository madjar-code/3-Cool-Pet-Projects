import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import * as S from './LoginRegisterModal.styled'
import RightArrowImage from '../../assets/images/LoginRegisterModal/RightArrowImage.svg'
import CloseButtonImage from '../../assets/images/LoginRegisterModal/CloseButtonImage.svg'
import AuthContext from '../../context/AuthContext'


const LoginRegisterModal = ({ modalState, setModalState }) => {
  const { loginUser } = useContext(AuthContext)
  const [credentials, setCredentials] =
    useState({email: '', password: ''})
  let modalContent = null
  let bottomButton = null

  const [valid, setValid] = useState(true)
  const navigate = useNavigate()

  const handleEmailChange = (e) => {
    setCredentials({...credentials, email: e.target.value })
  }

  const handlePasswordChange = (e) => {
    setCredentials({ ...credentials, password: e.target.value })
  }

  const handleLoginClick = () => {
    setValid(true)
    loginUser(credentials).then(
      status => {
        if (status === 200){
          setModalState('no modal')
        }
        else {
          setValid(false)
        }
      }
    )
  }

  if (modalState === 'login'){
    modalContent = 
      <>
        <S.Title>Login</S.Title>
        <S.Input
          placeholder="Почта..."
          onChange={(e) => handleEmailChange(e)}/>
        <S.Input
          placeholder="Пароль..." type="password"
          onChange={(e) => handlePasswordChange(e)}/>
        {!valid && <S.ErrorMessage>Incorrect email or password</S.ErrorMessage>}
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
        <S.Input placeholder='Username...'/>
        <S.Input placeholder='Email...'/>
        <S.Input placeholder='Password...'/>
        <S.Input placeholder='Confirm password...'/>
        <S.RegisterButton>Sign up!</S.RegisterButton>
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