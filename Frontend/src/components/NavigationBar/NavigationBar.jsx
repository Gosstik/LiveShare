import Sidebar from "../Sidebar/Sidebar";
import { SidebarItem } from "../Sidebar/Sidebar";

import { BarChart3, Package, Receipt, Settings } from "lucide-react";

const iconSize = 20;

export default function NavigationBar() {
  return (
    <Sidebar>
      <SidebarItem text="" icon={<BarChart3 size={iconSize}/>} active/>
      <SidebarItem text="" icon={<Package size={iconSize}/>} />
      <SidebarItem text="" icon={<Receipt size={iconSize}/>} alert/>
      <SidebarItem text="" icon={<Settings size={iconSize}/>} />
    </Sidebar>
  );
}
