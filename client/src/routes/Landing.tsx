import React, { useEffect } from 'react';
import CoverButton from "../components/CoverButton";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from "react-router-dom";

interface LandingProps {
  setMonochrome: (value: boolean) => void;
}

const Landing: React.FC<LandingProps> = ({ setMonochrome }) => {
  const navigate = useNavigate();
  const { isAuthenticated, loginWithPopup } = useAuth0();

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/generator");
    }
    setMonochrome(false);
  }, [isAuthenticated, navigate, setMonochrome]);

  return (
    <>
      <div className="w-full h-full flex flex-col items-center justify-center gap-15">
        <img className="max-w-[80%]" src="/img/logo.svg" alt="Mathwhiz.biz" />
        <CoverButton content="Join the Fun!" onClick={loginWithPopup} />
      </div>
    </>
  );
};

export default Landing;
