import { useState } from 'react'
import * as S from './CreateNote.styled'
import Header from '../../components/Header/Header'
import ErrorMessage from '../../components/ErrorMessage/ErrorMessage'


const CreateNote = () => {
  const MAX_TEXT_LENGTH = 2000
  const [text, setText] = useState('')
  const [showErrorMessage, setShowErrorMessage] = useState(false);
  const [errorText, setErrorText] = useState('')

  const textColor = text.length > MAX_TEXT_LENGTH ?
   'var(--warning-red)' : 'inherit';

  const handleCreateNote = () => {
    if (text.length == 0){
      setShowErrorMessage(true)
      setErrorText("Note can't be blank!")
    }
    else if (text.length > MAX_TEXT_LENGTH) {
      setShowErrorMessage(true);
      setErrorText('Note is too long!')
    }
    else {
      // Create Note
    }
  };

  const handleCloseErrorMessage = () => {
    setShowErrorMessage(false)
  }

  return (
    <S.Container>
      <Header/>
      <S.Content>
        <S.TextContainer>
          <S.TextCounter color={textColor}>
            {text.length}/{MAX_TEXT_LENGTH}
          </S.TextCounter>
          <S.TextField placeholder='Write your note...'
            onChange={(e) => setText(e.target.value)}/>
        </S.TextContainer>
        <S.SettingsContainer>
          <S.SettingsTitle>Optional Settings</S.SettingsTitle>
          <S.ParameterContainer>
            <S.ParameterName>Note Title</S.ParameterName>
            <S.NameInput placeholder='Note title...'/>
          </S.ParameterContainer>
          <S.ParameterContainer>
            <S.ParameterName>Expiration Time</S.ParameterName>
            <S.TimeSelect>
            <S.TimeOption value="null">None</S.TimeOption>
              <S.TimeOption value="10">10 minutes</S.TimeOption>
              <S.TimeOption value="60">1 hour</S.TimeOption>
              <S.TimeOption value="120">2 hours</S.TimeOption>
              <S.TimeOption value="360">6 hours</S.TimeOption>
              <S.TimeOption value="1440">24 hours</S.TimeOption>
            </S.TimeSelect>
          </S.ParameterContainer>
        </S.SettingsContainer>
        {showErrorMessage && <ErrorMessage text={errorText}
                               handleClose={handleCloseErrorMessage}/>}
        <S.CreateButton onClick={handleCreateNote}>
          Create Note!
        </S.CreateButton>
      </S.Content>
    </S.Container>
  )
}

export default CreateNote