// TODO: blackout

import React, { useState, useRef, useEffect } from "react";

import classNames from "classnames/bind";

import { Settings } from "lucide-react";

import style from "./Sidebar.module.scss";
import { current } from "@reduxjs/toolkit";

const cx = classNames.bind(style);

// export default function TopNavMenu() {
//   return (
//     <body>
//       <header>
//         <section className={style.headerTitleLine}>
//           <h1 className={style.headerTitle}>Acme Co.</h1>
//           <button className={style.menuButton}>
//             <div className={style.menuIcon}></div>
//           </button>
//         </section>

//         <div className={style.aboveNav}>
//           <nav>
//             <ul>
//               <li>
//                 <a href="#">Products</a>
//               </li>
//               <li>
//                 <a href="#">Forum</a>
//               </li>
//               <li>
//                 <a href="#">About</a>
//               </li>
//               <li>
//                 <a href="#">Contact</a>
//               </li>
//             </ul>
//           </nav>
//         </div>
//       </header>
//     </body>
//   );
// }

export default function Sidebar({ children }) {
  // add event listeners
  // TODO: check mouse already on Sidebar
  // console.log("reinit component");
  const [isSidebarOpened, setIsSidebarOpened] = useState(false);
  // console.log(`isSidebarOpened=${isSidebarOpened}`);
  const sidebar = useRef(null);

  const openSidebar = () => {
    console.log("OPEN SIDEBAR");
    sidebar.current.classList.add("opened");
    setIsSidebarOpened(true);
  };
  const closeSidebar = () => {
    if (isSidebarOpened) {
      console.log("CLOSE SIDEBAR");
      sidebar.current.classList.remove("opened");
      setIsSidebarOpened(false);
    }
  };

  useEffect(() => {
    const sidebarElem = sidebar.current;
    sidebarElem.addEventListener("mouseenter", openSidebar);
    sidebarElem.addEventListener("mouseleave", closeSidebar);
    return () => {
      sidebarElem.removeEventListener("mouseenter", openSidebar);
      sidebarElem.removeEventListener("mouseleave", closeSidebar);
    };
  }, [sidebar, isSidebarOpened]);

  return (
    <div
      className={cx(style.sidebar, { opened: isSidebarOpened })}
      ref={sidebar}
    >
      <div className={style.menuButtonBlock}>
        <div className={style.menuButton}>
          <div className={style.menuIcon}></div>
        </div>
      </div>
      <ul>
        <li>
          <a href="#">Home</a>
        </li>
        <li>
          <a href="#">Posts</a>
        </li>
        <li>
          <a href="#">Search Posts</a>
        </li>
        <li>
          <a href="#">Friends</a>
        </li>
      </ul>
    </div>
  );
}
