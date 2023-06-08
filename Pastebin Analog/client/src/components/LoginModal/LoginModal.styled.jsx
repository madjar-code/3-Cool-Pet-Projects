import styled from "styled-components";


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
`;

export const Title = styled.h3`
  text-align: center;
  font-weight: var(--medium);
  font-size: 22px;
  margin-top: 12.5px;
  opacity: 0.8;
`;

export const Modal = styled.div`
  max-width: 320px;
  height: 210px;
  background-color: var(--bgc-color);
  border-radius: 10px;
  padding-left: 10px;
  padding-right: 10px;
  box-shadow: 0px 0px 4px rgba(0, 0, 0, 0.25);
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

export const Button = styled.button`
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

export const RightArrow = styled.img`
`