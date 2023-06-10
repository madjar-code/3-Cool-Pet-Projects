import { useState } from 'react'
import * as S from './CreateNote.styled'
import Header from '../../components/Header/Header'
import ErrorMessage from '../../components/ErrorMessage/ErrorMessage'
import APIService from '../../API/APIService'
import LoginRegisterModal from '../../components/LoginRegisterModal/LoginRegisterModal'


const CreateNote = () => {
  const MAX_TEXT_LENGTH = 2000
  const [showErrorMessage, setShowErrorMessage] = useState(false);
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);
  const [modalState, setModalState] = useState('no modal')
  const [errorText, setErrorText] = useState('')

  const [credentials, setCredentials] = useState(
    {
      title: null,
      text: '',
      time_delta: null,
    }
  )

  const textColor = credentials.text.length > MAX_TEXT_LENGTH ?
   'var(--warning-red)' : 'inherit';

  const handleCreateNote = () => {
    if (credentials.text.length == 0){
      setShowErrorMessage(true)
      setErrorText("Note can't be blank!")
    }
    else if (credentials.text.length > MAX_TEXT_LENGTH) {
      setShowErrorMessage(true);
      setErrorText('Note is too long!')
    }
    else {
      setShowErrorMessage(false)
      setIsButtonDisabled(true);
      APIService.createNote(credentials)
      .then(data => {
        setTimeout(() => {
          setIsButtonDisabled(false);
        }, 10000);
      });
    }
  };

  const handleCloseErrorMessage = () => {
    setShowErrorMessage(false)
  }

  const handleTitleChange = (e) => {
    setCredentials({ ...credentials, title: e.target.value });
  };

  const handleTextChange = (e) => {
    setCredentials({ ...credentials, text: e.target.value });
  };

  const handleTimeDeltaChange = (e) => {
    const value = e.target.value === "null" ? null : parseInt(e.target.value, 10);
    setCredentials({ ...credentials, time_delta: value });
  };

  return (
    <S.Container>
      <Header setModalState={setModalState}/>
      <S.Content>
        <S.TextContainer>
          <S.TextCounter color={textColor}>
            {credentials.text.length}/{MAX_TEXT_LENGTH}
          </S.TextCounter>
          <S.TextField placeholder='Write your note...'
            onChange={handleTextChange}/>
        </S.TextContainer>
        <S.SettingsContainer>
          <S.SettingsTitle>Optional Settings</S.SettingsTitle>
          <S.ParameterContainer>
            <S.ParameterName>Note Title</S.ParameterName>
            <S.NameInput
              placeholder="Note title..."
              onChange={handleTitleChange}
            />
          </S.ParameterContainer>
          <S.ParameterContainer>
            <S.ParameterName>Expiration Time</S.ParameterName>
            <S.TimeSelect onChange={handleTimeDeltaChange}>
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
        <S.CreateButton
            onClick={handleCreateNote}
            disabled={isButtonDisabled}
          >
          Create Note!
        </S.CreateButton>
      </S.Content>
      { modalState !== 'no modal' && <LoginRegisterModal modalState={modalState}
                                        setModalState={setModalState}/>}
    </S.Container>
  )
}

export default CreateNote