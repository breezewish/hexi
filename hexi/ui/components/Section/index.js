import Section from './Section';
import SectionContainer from './SectionContainer';
import SectionContent from './SectionContent';

export default {
  install(Vue) {
    Vue.component(Section.name, Section);
    Vue.component(SectionContainer.name, SectionContainer);
    Vue.component(SectionContent.name, SectionContent);
  },
};
