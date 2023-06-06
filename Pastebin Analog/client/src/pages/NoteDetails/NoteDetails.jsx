import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import * as S from './NoteDetails.styled'
import Header from '../../components/Header/Header'
import APIService from '../../API/APIService'


const NoteDetails = () => {
  const [note, setNote] = useState()
  const params = useParams()

  useEffect(() => {
    APIService.getNoteDetails(params.hash).then(
      data => setNote(data))
  }, [params.hash])

  return (
    <S.Container>
      <Header/>
      <S.Content>

      </S.Content>
    </S.Container>
  )
}


export default NoteDetails