import * as S from './ErrorMessage.styled'
import WarniningIconImage from '../../assets/images/ErrorMessage/WarningIconImage.svg'
import CloseIcon from '@mui/icons-material/Close';

const IconStyle = {
  position: 'absolute',
  right: '2px',
  height: '20px',
  width: '20px',
}


const ErrorMessage = ({ text, handleClose }) => {
  return (
    <S.Container>
      <S.WarningIcon src={WarniningIconImage}/>
      <S.Label>{text}</S.Label>
      <CloseIcon style={IconStyle} onClick={handleClose}/>
    </S.Container>
  )
}

export default ErrorMessage