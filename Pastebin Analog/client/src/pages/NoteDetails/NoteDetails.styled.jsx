import styled from 'styled-components'


export const Container = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh; 
`;

export const Content = styled.div`
  flex: 1;
  padding-left: 15px;
  padding-right: 15px;
`;

export const Title = styled.h2`
  padding-left: 5px;
  margin-top: 15px;
  font-size: 22px;
  font-weight: var(--bold);
`

export const TextContainer = styled.div`
  margin-top: 15px;
  background-color: var(--front-color);
  border-radius: 5px;
  padding: 5px;
`

export const MetadataContainer = styled.div`
  margin-top: 15px;
  border-radius: 5px;
  padding: 8px;
  display: flex;
  justify-content: center;
  width: 250px;
  background-color: var(--front-color);
`

export const MetadataWrapper = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
`

export const CreationDateWrapper = styled.div`
  display: flex;
  align-items: center;
`

export const Icon = styled.img`
  margin-right: 4px;
`

export const CreationDate = styled.p`
  margin-right: 15px;
`

export const TimeDeltaWrapper = styled.div`
  display: flex;
  align-items: center;
`

export const TimeDelta = styled.p`
  margin-right: 15px;
`

export const CountOfViewsWrapper = styled.div`
  display: flex;
  align-items: center;
`

export const CountOfViews = styled.p`
`

export const LinkContainer = styled.div`
  margin-top: 30px;
  height: 30px;
  background-color: var(--front-color);
  display: grid;
  grid-template-columns: 1fr 95px;
`

export const Link = styled.div`
  font-size: 16px;
  margin-top: 5px;
  text-align: center;
`

export const LinkButton = styled.button`
  width: 95px;
  height: 30px;
  border-radius: 0 5px 5px 0;
  background-color: var(--dark-grey);
`
