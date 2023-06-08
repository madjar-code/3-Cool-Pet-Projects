import * as S from './RegisterModal.styled'
import RightArrowImage from '../../assets/images/LoginModal/RightArrowImage.svg'


const RegisterModal = () => {
  return (
    <S.Container>
      <S.Modal>
        <S.Title>Register</S.Title>
        <S.Input placeholder='Username...'/>
        <S.Input placeholder='Email...'/>
        <S.Input placeholder='Password...'/>
        <S.Input placeholder='Confirm password...'/>
        <S.Button>Sign up!</S.Button>
      </S.Modal>
      <S.ButtonWrapper>
        <S.ToLoginButton>
          or login
          <S.RightArrow src={RightArrowImage}/>
        </S.ToLoginButton>
      </S.ButtonWrapper>
    </S.Container>
  )
}

export default RegisterModal