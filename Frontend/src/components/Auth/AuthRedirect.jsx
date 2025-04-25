import { useEffect, useState } from "react";

import { authUrl } from "../../api/urls";

export default function AuthRedirect() {
  console.log("AuthSuccess start");

  useEffect(() => {
    const script = document.createElement("script");

    script.src =
      "https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-token-with-polyfills-latest.js";
    script.async = true;

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  //////////////////////////////////

  console.log("AuthSuccess before YaSendSuggestToken");

  // window.YaSendSuggestToken('http://localhost:3000/auth')

  if (!window.YaSendSuggestToken) {
    console.log(`!!! NOT AN OBJECT`)
    console.log(`window.YaSendSuggestToken=${window.YaSendSuggestToken}`)
    return <div>NOT AN OBJECT</div>;
  }

  window.YaSendSuggestToken(`http://localhost:3000${authUrl}`, {
    flag: true,
    kek: true,
  });

  console.log("AuthSuccess after YaSendSuggestToken");

  return <div></div>;
}
