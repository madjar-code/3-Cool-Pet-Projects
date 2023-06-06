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

export const TextContainer = styled.div`
  margin-top: 25px;
  height: 250px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
`;

export const TextCounter = styled.p`
  color: ${props => props.color};
`;

export const TextField = styled.textarea`
  outline: none;
  resize: none;
  margin-top: 5px;
  flex: 1;
  background-color: var(--bgc-color);
  padding: 10px;
  border-radius: 5px;
  border: 1px solid var(--text-color);
  box-sizing: border-box;
  transition: border 0.5s ease, box-shadow 0.5s ease, background-color 1s ease;

  &:focus {
    border-color: transparent;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
    background-color: var(--front-color);
  }

  &::placeholder{
    opacity: 0.6;
  }
`;

export const SettingsContainer = styled.div`
`

export const SettingsTitle = styled.h3`
  margin-top: 30px;
  padding-bottom: 5px;
  font-size: 20px;
`

export const ParameterContainer = styled.div`
  margin-top: 18px;
  display: grid;
  grid-template-columns: 140px 1fr;
`

export const ParameterName = styled.p`
  font-size: 15px;
`

export const NameInput = styled.input`
  border-radius: 5px;
  background-color: var(--bgc-color);
  height: 24px;
  min-width: 50px;
  padding-left: 7px;
  border: 1px solid var(--text-color);
`

export const TimeSelect = styled.select`
  height: 25px;
  padding-left: 5px;
  border-radius: 5px;
  background-color: var(--front-color);
`

export const TimeOption = styled.option`
`

export const CreateButton = styled.button`
  margin-top: 40px;
  position: relative;
  left: 50%;
  margin-left: -70px;
  width: 140px;
  height: 35px;
  font-size: 17px;
  background-color: var(--front-color);
  border-radius: 10px;
  box-shadow: var(--simple-shadow);
  transition: 500ms;

  &:hover {
    background-color: var(--dark-grey);
    box-shadow: none;
  }
`
