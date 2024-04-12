type MenuItem = {
  name: string;
  link: string;
  icon: string;
};

export const menuItems: Array<MenuItem> = [
  {
    name: 'Översikt',
    link: '/overview',
    icon: 'bi-caret-right-square-fill'
  } as MenuItem,
  {
    name: 'Mögelrisk',
    link: '/mould_risk',
    icon: 'bi-graph-up-arrow'
  } as MenuItem,
  {
    name: 'Vattenmängd',
    link: '/water_content',
    icon: 'bi-graph-up-arrow'
  } as MenuItem,
  {
    name: 'Start',
    link: '/',
    icon: 'bi-info-circle-fill'
  } as MenuItem
];
