import moment from 'moment';
import { useEffect, useState, useRef, useContext } from 'react'
import { useParams } from 'react-router-dom'
import * as S from './NoteDetails.styled'
import Header from '../../components/Header/Header'
import APIService from '../../API/APIService'
import CalendarIconImage from '../../assets/images/NoteDetails/CalendarIconImage.svg'
import TimeIconImage from '../../assets/images/NoteDetails/TimeIconImage.svg'
import EyeIconImage from '../../assets/images/NoteDetails/EyeIconImage.svg'
import LoginRegisterModal from '../../components/LoginRegisterModal/LoginRegisterModal';
import AuthContext from '../../context/AuthContext';
import EditNoteImage from '../../assets/images/NoteDetails/EditNoteImage.svg'
import DeleteNoteIcon from '../../assets/images/NoteDetails/DeleteNoteImage.svg'


const NoteDetails = () => {
  const [note, setNote] = useState()
  const [copied, setCopied] = useState(false);
  const [modalState, setModalState] = useState('no modal')
  const {user} = useContext(AuthContext)
  const linkRef = useRef(null)
  const params = useParams()

  useEffect(() => {
    if (!note) {
      APIService.getNoteDetails(params.hash).
        then(data => setNote(data));
    }
  }, [params.hash, note])

  const isAuthor = () => {
    return user?.user_id == note?.author
  }

  const formatTimeDelta = (hours, minutes) => {
    let timeDelta = ''
    if (hours > 0) {
      timeDelta += `${hours} ${hours === 1 ? 'h' : 'h'}`;
    }
    else if (minutes > 0 ||  hours < 2) {
      timeDelta += ` ${minutes} ${minutes === 1 ? 'm' : 'm'}`;
    }
    return timeDelta.trim();
  }

  const getTimeDelta = () => {
    if (note && note?.expiration_time) {
      const expirationTime = moment(note.expiration_time, 'DD.MM.YYYY HH:mm:ss');
      const currentTime = moment();
      const duration = moment.duration(expirationTime.diff(currentTime));
      const hours = Math.floor(duration.asHours());
      const minutes = Math.floor(duration.asMinutes() % 60);
      return formatTimeDelta(hours, minutes);
    }
    return 'Never'
  };

  if (!note) {
    return null;
  }

  const handleEditClick = () => { 
  }

  const handleDeleteClick = () => { 
  }

  const handleCopyLink = () => {
    if (linkRef.current) {
      const range = document.createRange();
      range.selectNode(linkRef.current);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
      document.execCommand('copy');
      window.getSelection().removeAllRanges();
      setCopied(true);
      setTimeout(() => {
        setCopied(false);
      }, 1500);
    }
  };

  return (
    <S.Container>
      <Header setModalState={setModalState}/>
      <S.Content>
        { note?.title && <S.Title>{note?.title}</S.Title>}
        <S.TextContainer>{note?.text}</S.TextContainer>
        <S.MetadataContainer>
          <S.MetadataWrapper>
          <S.CreationDateWrapper>
              <S.Icon src={CalendarIconImage}/>
              <S.CreationDate>{note?.created_at}</S.CreationDate>
            </S.CreationDateWrapper>
            <S.TimeDeltaWrapper>
              <S.Icon src={TimeIconImage}/>
              <S.TimeDelta>{getTimeDelta()}</S.TimeDelta>
            </S.TimeDeltaWrapper>
            <S.CountOfViewsWrapper>
              <S.Icon src={EyeIconImage}/>
              <S.CountOfViews>{note?.view_count}</S.CountOfViews>
            </S.CountOfViewsWrapper>
          </S.MetadataWrapper>
        </S.MetadataContainer>
        <S.LinkContainer>
          <S.Link ref={linkRef}>notify.com/{note?.hash}</S.Link>
          <S.LinkButton onClick={handleCopyLink} copied={copied}>
            {copied ? "Copied!" : "Copy Link!"}
          </S.LinkButton>
        </S.LinkContainer>
        {
          isAuthor() && 
          <S.ButtonContainer>
            <S.EditButton onClick={handleEditClick}>
              <S.EditIcon src={EditNoteImage}/>
            </S.EditButton>
            <S.DeleteButton onClick={handleDeleteClick}>
              <S.DeleteIcon src={DeleteNoteIcon}/>
            </S.DeleteButton>
          </S.ButtonContainer>
    
        }
      </S.Content>
      { modalState !== 'no modal' && <LoginRegisterModal modalState={modalState}
                                        setModalState={setModalState}/>}
    </S.Container>
  )
}


export default NoteDetails