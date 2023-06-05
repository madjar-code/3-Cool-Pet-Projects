import * as S from './Header.styled'
import MenuButtonImage from '../../assets/images/Header/MenuButtonImage.svg'


const Header = () => {
  return (
    <S.Container>
      <S.Wrapper>
        <S.MenuButton src={MenuButtonImage}/>
        <S.Logo>Notify</S.Logo>
      </S.Wrapper>
    </S.Container>
  )
}

export default Header