import { useContext } from 'react'
import * as S from './Header.styled'
import MenuButtonImage from '../../assets/images/Header/MenuButtonImage.svg'
import LoginButtonImage from '../../assets/images/Header/LoginButtonImage.svg'
import LogoutButtonImage from '../../assets/images/Header/LogoutButtonImage.svg'
import AuthContext from '../../context/AuthContext'


const Header = ({ setModalState }) => {
  const { user, logoutUser } = useContext(AuthContext)

  return (
    <S.Container>
      <S.Wrapper>
        <S.MenuButton src={MenuButtonImage}/>
        <S.Logo>Noter</S.Logo>
        { user ? (
          <S.LogoutButton src={LogoutButtonImage}
            onClick={() => logoutUser()}/>
        ) : (
          <S.LoginButton src={LoginButtonImage}
            onClick={() => setModalState('login')}/>
        )}
      </S.Wrapper>
    </S.Container>
  )
}

export default Header