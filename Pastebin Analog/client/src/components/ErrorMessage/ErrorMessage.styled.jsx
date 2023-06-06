import styled, { keyframes } from "styled-components";


const slideInAnimation = keyframes`
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(0);
  }
`

export const Container = styled.div`
  margin-top: 25px;
  position: relative;
  height: 30px;
  border-radius: 5px;
  border: 1px solid var(--warning-red);
  color: var(--warning-red);

  animation: ${slideInAnimation} 0.3s ease-in;
  transition: transform 0.3s ease-out;

  display: flex;
  flex-direction: row;
  align-items: center;
`

export const WarningIcon = styled.img`
  margin-left: 2px;
`

export const Label = styled.div`
  margin-left: 5px;
`