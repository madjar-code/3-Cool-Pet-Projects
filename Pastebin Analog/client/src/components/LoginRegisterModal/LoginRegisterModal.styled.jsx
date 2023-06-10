import styled, { keyframes } from "styled-components";


export const Title = styled.h3`
  text-align: center;
  font-weight: var(--medium);
  font-size: 22px;
  opacity: 0.8;
`;

export const Container = styled.div`
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  opacity: 0;
  animation: fadeIn 0.5s forwards;
  /* animation-delay: 0.5s; */

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
`;

export const Modal = styled.div`
  position: relative;
  max-width: 320px;
  background-color: var(--bgc-color);
  border-radius: 10px;
  padding-top: 15px;
  padding-bottom: 15px;
  padding-left: 10px;
  padding-right: 10px;
  box-shadow: 0px 0px 0px rgba(0, 0, 0, 0.25);
  animation: slideIn 0.5s forwards;

  @keyframes slideIn {
    from {
      box-shadow: 0px 0px 0px rgba(0, 0, 0, 0);
      transform: translateX(-100%);
    }
    to {
      box-shadow: 0px 0px 4px rgba(0, 0, 0, 0.25);
      transform: translateX(0%);
    }
  }
`;

export const Input = styled.input`
  width: 100%;
  margin-top: 20px;
  height: 32px;
  border-radius: 5px;
  outline: none;
  background-color: var(--bgc-color);
  padding: 10px;
  border: 1px solid var(--text-color);
  box-sizing: border-box;
  transition: border 0.35s ease, box-shadow 0.35s ease, background-color 1s ease;

  &:focus {
    border-color: transparent;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
    background-color: var(--front-color);
  }

  &::placeholder{
    opacity: 0.6;
  }
`;

export const LoginButton = styled.button`
  margin-top: 25px;
  position: relative;
  left: 50%;
  margin-left: -60px;
  width: 120px;
  height: 25px;
  font-size: 16px;
  background-color: var(--front-color);
  border-radius: 12.5px;
  box-shadow: var(--simple-shadow);
  transition: 200ms;

  &:hover {
    background-color: var(--dark-grey);
    box-shadow: none;
  }
`

export const RegisterButton = styled(LoginButton)`
`

export const CloseButton = styled.img`
  position: absolute;
  top: 10px;
  right: 10px;
`

export const ButtonWrapper = styled.div`
  margin-top: 10px;
  width: 100%;
  max-width: 320px;
  display: flex;
  justify-content: flex-end;
`

export const ToRegisterButton = styled.button`
  background-color: var(--bgc-color);
  width: 110px;
  height: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  padding-left: 15px;
`;

export const ToLoginButton = styled.button`
  background-color: var(--bgc-color);
  width: 90px;
  height: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  padding-left: 15px;
`;

export const RightArrow = styled.img`
`