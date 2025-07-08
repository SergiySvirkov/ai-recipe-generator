Phase 5: Responsive Design Strategy

<!-- This document explains the approach taken to make the application's UI responsive. -->
1. Core Principles

Our responsive design strategy is built on two core CSS features:

    Flexbox Layout: The main layout of the application (specifically the HomePage component containing the form and the recipe display) is built using display: flex. This allows elements to flexibly grow, shrink, and wrap, which is ideal for creating layouts that adapt to different screen sizes.

    Media Queries: We use CSS media queries (@media) to apply specific styles only when the browser window is within a certain width range. This allows us to make targeted adjustments for different device categories like tablets and mobile phones.

2. Breakpoints

We have defined two primary breakpoints for our design:

    992px (Tablet and below): This is the point where the main two-column layout (form on the left, recipe on the right) becomes too crowded. When the screen width is 992px or less, the layout switches to a single vertical column.

    576px (Mobile and below): This breakpoint targets smaller mobile devices. Here, we make finer adjustments to save space and improve readability, such as:

        Reducing padding on all major containers (Navbar, HomePage, etc.).

        Making fonts slightly smaller.

        Stacking elements within the Navbar vertically.

3. Implementation Details (styles.css)
homepage-container

    Desktop: display: flex with flex-wrap: wrap creates a side-by-side layout.

    Tablet/Mobile (max-width: 992px): We change flex-direction: column to stack the form and recipe display vertically.

form-container & recipe-display-container

    Desktop: We use flex-basis and flex-grow to define their relative sizes in the flex container.

    Tablet/Mobile (max-width: 992px): We set flex-basis: 100% to make them take up the full available width within the new single-column layout.

Navbar & General Padding

    Mobile (max-width: 576px): We reduce the padding on the navbar and other containers to maximize the usable screen space. The navbar's content is also stacked vertically to prevent awkward horizontal crowding.

This "mobile-first" thinking (or in this case, "desktop-first with graceful degradation") ensures that the application is usable and looks professional on any device a user might have.
