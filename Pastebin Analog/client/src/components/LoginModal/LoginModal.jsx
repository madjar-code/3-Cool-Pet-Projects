import * as S from './LoginModal.styled'
import RightArrowImage from '../../assets/images/LoginModal/RightArrowImage.svg'


const LoginModal = () => {
  return (
    <S.Container>
      <S.Modal>
        <S.Title>Login</S.Title>
        <S.Input placeholder='Email...'/>
        <S.Input placeholder='Password...'/>
        <S.Button>Log in!</S.Button>
      </S.Modal>
      <S.ButtonWrapper>
        <S.ToRegisterButton>
          or register
          <S.RightArrow src={RightArrowImage}/>
        </S.ToRegisterButton>
      </S.ButtonWrapper>
    </S.Container>
  )
}

export default LoginModal