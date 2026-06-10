<template>
  <BasePage :navBarVariant="navBarControl">
    <div class="p-8 sm:p-12 sm:my-12 lg:p-20 lg:my-6 text-text-main">
      <h2 class="text-title text-3xl sm:text-5xl font-bold mb-8 self-center">Terms of Services</h2>
      <span class="my-12">
        <span class="important">Effective Date: May 26, 2026</span><br>
        Website: Ft_cat (https://localhost:1443)<br>
        <span class="text-title text-2xl font-bold">Welcome to Ft_cat !</span><br>
        This website is an <span class="important">academic school project</span> developed for <span class="important">educational purposes only</span>. By accessing or using our local service, you agree to comply with and be bound by these Terms of Service. <span class="important">If you do not agree, please do not create an account or use the site.</span>
      </span>
      <ul>
        <li>
          <h3>1. Description of Service</h3>
          <p>
            <span class="important">Ft_cat</span> is a <span class="important">non-commercial school project</span> hosted locally. It <span class="important">does not</span> sell any products, offer subscriptions, run promotions, or engage in any commerce. Access to the website's content <span class="important">requires the creation of a user profile</span>.
          </p>
        </li>
        <li>
          <h3>2. Account Creation & Security</h3>
          <p>
            To access the content, <span class="important">you must create a user profile</span>.<br>
            <span class="important">You are responsible</span> for maintaining the confidentiality of your login credentials.<br>
            Since this is a local development project, security is provided via a local SSL certificate, but <span class="important">the platform should not be used to store sensitive real-world passwords</span>.
          </p>
        </li>
        <li>
          <h3>3. User-Generated Content</h3>
          <p>
            Users may upload content, specifically profile pictures (photos).<br>
            <span class="important">You retain ownership of any photos you upload</span>, but by uploading them, you grant Ft_cat a temporary, royalty-free license to display them within the local application.<br>
            <span class="important">You agree not to upload any illegal, offensive, or copyrighted material that you do not have permission to use.</span>
          </p>
        </li>
        <li>
          <h3>4. Intellectual Property & Assets</h3>
          <p>
            The logos, graphics, and other visual assets used on Ft_cat <span class="important">do not</span> belong to the website creators.<br>
            These assets have been sourced from the internet or generated via Artificial Intelligence (AI) for educational demonstration purposes only.<br>
            <span class="important">No copyright infringement is intended</span>. If you recognize any asset and wish for it to be removed, please note that this site is not publicly indexed or commercially deployed.
          </p>
        </li>
        <li>
          <h3>5. Limitation of Liability & "As-Is" Status</h3>
          <p>
            Ft_cat is provided on an <span class="important">"AS IS"</span> and <span class="important">"AS AVAILABLE"</span> basis.<br>
            We make no warranties regarding the stability, uptime, or permanent data storage of this website.<br>
            As a student project, <span class="important">the creators are not liable for any data loss, bugs, or security vulnerabilities</span>
          </p>
        </li>
        <li>
          <h3>6. Feedback and Contact</h3>
          <p>
            This website <span class="important">does not</span> feature a live system to receive, process, or respond to user feedback.<br>
            There is no dedicated physical address or support email address monitoring queries regarding these Terms of Service.
          </p>
        </li>
      </ul>
    </div>
  </BasePage>
</template>


<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';

const scrollY = ref(0);
const navBarControl = computed(() => scrollY.value <= 0 ? 'home' : 'nav');

function handleScroll() {
  scrollY.value = window.scrollY
  console.log(navBarControl.value);
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
})
</script>

<style scoped>
@import "@/style.css";

li {
  @apply my-6
}
h3 {
  @apply text-title text-2xl font-semibold mb-3
}
br {
  @apply mb-4
}
p {
  @apply pl-4
}

.important {
  @apply font-black italic
}
</style>
