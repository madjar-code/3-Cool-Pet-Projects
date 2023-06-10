import * as S from './Header.styled'
import MenuButtonImage from '../../assets/images/Header/MenuButtonImage.svg'
import LoginButtonImage from '../../assets/images/Header/LoginButtonImage.svg'

const Header = ({ setModalState }) => {
  return (
    <S.Container>
      <S.Wrapper>
        <S.MenuButton src={MenuButtonImage}/>
        <S.Logo>Notify</S.Logo>
        <S.LoginButton src={LoginButtonImage}
          onClick={() => setModalState('login')}/>
      </S.Wrapper>
    </S.Container>
  )
}

export default Header