import * as S from './LoginRegisterModal.styled'
import RightArrowImage from '../../assets/images/LoginRegisterModal/RightArrowImage.svg'
import CloseButtonImage from '../../assets/images/LoginRegisterModal/CloseButtonImage.svg'


const LoginRegisterModal = ({ modalState, setModalState }) => {
  let modalContent = null
  let bottomButton = null

  if (modalState === 'login'){
    modalContent = 
      <>
        <S.Title>Login</S.Title>
        <S.Input placeholder='Email...'/>
        <S.Input placeholder='Password...'/>
        <S.LoginButton>Log in!</S.LoginButton>
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