from difflib import get_close_matches
from typing import Dict, List, Optional
import re

class CDPKnowledgeBase:
    def __init__(self):
        # Simplified document structure with clear categories and more keywords
        self.documents = {
            'segment_source': {
                'title': 'Setting up a Source in Segment',
                'keywords': [
                    'source', 'segment', 'setup', 'tracking', 'collect', 'data', 
                    'add source', 'new source', 'create source', 'configure source',
                    'how to source', 'segment source', 'data source'
                ],
                'content': """
                To set up a new source in Segment:
                1. Log in to your Segment workspace
                2. Go to Connections > Sources in the left navigation
                3. Click "Add Source" button
                4. Select your source type (Website, Mobile App, Server, etc.)
                5. Name your source and click "Add Source"
                6. Follow the source-specific setup instructions
                7. Configure your settings and preferences
                8. Enable the source when ready

                Common source types:
                • Analytics.js for websites
                • iOS/Android SDKs for mobile apps
                • Server-side libraries
                • Cloud sources for SaaS tools
                """
            },
            'mparticle_profile': {
                'title': 'Creating User Profiles in mParticle',
                'keywords': [
                    'profile', 'mparticle', 'user', 'identity', 'customer',
                    'create profile', 'user profile', 'customer profile',
                    'how to profile', 'mparticle profile', 'setup profile'
                ],
                'content': """
                To create and manage user profiles in mParticle:
                1. Implement identity management
                2. Set up user attributes
                3. Configure identity priority
                4. Define user identity mapping
                5. Enable cross-platform identity resolution

                Key concepts:
                • Customer IDs
                • Device IDs
                • User attributes
                • Identity resolution
                """
            },
            'lytics_audience': {
                'title': 'Building Audience Segments in Lytics',
                'keywords': [
                    'audience', 'lytics', 'segment', 'targeting', 'segmentation',
                    'create audience', 'build segment', 'audience segment',
                    'how to audience', 'lytics segment', 'setup audience'
                ],
                'content': """
                To build an audience segment in Lytics:
                1. Go to Audiences in your Lytics account
                2. Click "Create New Audience"
                3. Define segment criteria
                4. Set behavioral rules
                5. Add profile attributes
                6. Configure content affinities
                7. Set audience rules
                8. Save and activate

                Best practices:
                • Start with broad criteria
                • Use behavioral data
                • Test audience sizes
                • Monitor audience growth
                """
            },
            'zeotap_integration': {
                'title': 'Integrating Data with Zeotap',
                'keywords': [
                    'zeotap', 'integration', 'data', 'connect', 'setup', 'configure',
                    'how to integrate', 'zeotap integration', 'data integration'
                ],
                'content': """
                To integrate your data with Zeotap:
                1. Log in to your Zeotap account
                2. Navigate to the Integrations section
                3. Click "Add Integration"
                4. Select your data source type
                5. Follow the setup instructions for your specific source
                6. Configure your integration settings
                7. Test the integration to ensure data flow
                8. Activate the integration when ready

                Tips:
                • Ensure your data is clean and formatted correctly
                • Use Zeotap's data mapping tools for accurate integration
                • Monitor data flow regularly to catch any issues early
                """
            },
            'segment_advanced': {
                'title': 'Advanced Configurations in Segment',
                'keywords': [
                    'advanced', 'configuration', 'segment', 'custom', 'setup', 'tracking plan',
                    'protocols', 'data governance', 'schema', 'validation'
                ],
                'content': """
                Advanced configurations in Segment include:

                1. Setting up a Tracking Plan:
                   - Define your data schema
                   - Use Protocols to enforce data quality
                   - Validate incoming data against your schema

                2. Custom Destinations:
                   - Create custom integrations using Functions
                   - Use the Segment API for advanced data routing

                3. Data Governance:
                   - Implement data access controls
                   - Monitor data flow and quality

                Tips:
                • Regularly review and update your tracking plan
                • Use Segment's debugging tools to troubleshoot issues
                """
            },
            'mparticle_advanced': {
                'title': 'Advanced Integrations in mParticle',
                'keywords': [
                    'advanced', 'integration', 'mparticle', 'custom', 'setup', 'sdk',
                    'api', 'data pipeline', 'real-time', 'event processing'
                ],
                'content': """
                Advanced integrations in mParticle include:

                1. Real-time Event Processing:
                   - Use mParticle's SDKs for real-time data collection
                   - Implement custom event processing logic

                2. API Integrations:
                   - Use mParticle's API for custom data flows
                   - Integrate with third-party services

                3. Data Pipeline Management:
                   - Configure data routing and transformation
                   - Monitor data flow and performance

                Tips:
                • Leverage mParticle's developer resources for custom integrations
                • Test integrations thoroughly before deployment
                """
            },
            'lytics_advanced': {
                'title': 'Advanced Audience Building in Lytics',
                'keywords': [
                    'advanced', 'audience', 'lytics', 'segmentation', 'personalization',
                    'machine learning', 'predictive', 'scoring', 'content affinity'
                ],
                'content': """
                Advanced audience building in Lytics includes:

                1. Predictive Scoring:
                   - Use machine learning models to score users
                   - Predict user behavior and preferences

                2. Content Affinity:
                   - Analyze user interactions to determine content preferences
                   - Personalize content delivery based on affinity scores

                3. Dynamic Segmentation:
                   - Create segments that update in real-time
                   - Use behavioral data for precise targeting

                Tips:
                • Continuously refine your models for better accuracy
                • Use Lytics' insights to drive personalized marketing campaigns
                """
            }
        }

        # Add conversation patterns
        self.conversation_patterns = {
            r'hi|hello|hey': self._greeting_response,
            r'thank|thanks': self._thank_response,
            r'bye|goodbye': self._goodbye_response,
            r'help|assist': self._help_response,
            r'what can you do|what do you do': self._capabilities_response
        }

    def search(self, query: str) -> Dict:
        """Enhanced search with conversation handling"""
        query = query.lower().strip()
        
        # 1. Check for conversation patterns
        for pattern, response_func in self.conversation_patterns.items():
            if re.search(pattern, query):
                return response_func()

        # 2. Check for CDP-specific questions
        if 'cdp' in query or 'customer data platform' in query:
            return self._cdp_overview_response()

        # Check for Zeotap-specific questions
        if 'zeotap' in query:
            return self._format_response(self.documents['zeotap_integration'])

        # Check for advanced questions
        if 'advanced' in query:
            if 'segment' in query:
                return self._format_response(self.documents['segment_advanced'])
            elif 'mparticle' in query:
                return self._format_response(self.documents['mparticle_advanced'])
            elif 'lytics' in query:
                return self._format_response(self.documents['lytics_advanced'])

        # 1. Direct keyword matching with more lenient scoring
        best_match = self._find_best_match(query)
        if best_match:
            return self._format_response(best_match)

        # 2. Phrase matching
        for doc_id, doc in self.documents.items():
            if self._phrase_match(query, doc):
                return self._format_response(doc)

        # 3. Fuzzy matching with lower threshold
        for doc_id, doc in self.documents.items():
            if self._fuzzy_match(query, doc['content'].lower()):
                return self._format_response(doc)

        # 4. Return default response if no match found
        return self._get_default_response()

    def _find_best_match(self, query: str) -> Optional[Dict]:
        """Find best matching document based on keywords with improved scoring"""
        scores = {}
        query_words = set(query.split())
        
        for doc_id, doc in self.documents.items():
            score = 0
            # Check keywords with partial matching
            for keyword in doc['keywords']:
                if keyword in query:
                    score += 3  # Higher weight for exact keyword matches
                elif any(word in keyword for word in query_words):
                    score += 1  # Partial matches get lower weight

            # Check title words
            title_words = set(doc['title'].lower().split())
            score += len(query_words.intersection(title_words)) * 2
            
            scores[doc_id] = score

        # Get best match if score is above threshold (lowered threshold)
        best_doc_id = max(scores.items(), key=lambda x: x[1])
        if best_doc_id[1] > 0:
            return self.documents[best_doc_id[0]]
        return None

    def _phrase_match(self, query: str, doc: Dict) -> bool:
        """Match common phrases and variations"""
        phrases = [
            (f"how to {kw}", kw) for kw in doc['keywords']
        ] + [
            (f"how do i {kw}", kw) for kw in doc['keywords']
        ] + [
            (f"setup {kw}", kw) for kw in doc['keywords']
        ] + [
            (f"create {kw}", kw) for kw in doc['keywords']
        ]
        
        return any(phrase[0] in query for phrase in phrases)

    def _fuzzy_match(self, query: str, content: str) -> bool:
        """Use fuzzy matching with lower threshold"""
        query_words = query.split()
        content_words = content.split()
        
        matches = 0
        for word in query_words:
            if get_close_matches(word, content_words, n=1, cutoff=0.7):  # Lower cutoff
                matches += 1
        
        # Return True if more than 30% of query words match (lower threshold)
        return matches / len(query_words) >= 0.3

    def _format_response(self, doc: Dict) -> Dict:
        """Format document into response"""
        return {
            'title': doc['title'],
            'content': doc['content'].strip()
        }

    def _get_default_response(self) -> Dict:
        """Return default response when no match is found"""
        return {
            'title': 'How can I help you?',
            'content': """
            I can help you with:
            1. Setting up sources in Segment
            2. Creating user profiles in mParticle
            3. Building audience segments in Lytics

            Please try:
            • Being specific about which CDP you're asking about
            • Mentioning the feature you're interested in (source, profile, audience)
            • Using terms like "how to" or "setup"

            Example questions:
            • "How do I set up a source in Segment?"
            • "Creating user profiles in mParticle"
            • "Building audience segments in Lytics"
            """
        }

    def format_response(self, data: Dict) -> str:
        """Format the final response string"""
        return f"# {data['title']}\n\n{data['content']}" 

    # Add conversation handlers
    def _greeting_response(self) -> Dict:
        return {
            'title': 'Hello! 👋',
            'content': """
            Hi! I'm your CDP assistant. I can help you with:
            • Setting up sources in Segment
            • Creating user profiles in mParticle
            • Building audience segments in Lytics

            What would you like to know about?
            """
        }

    def _thank_response(self) -> Dict:
        return {
            'title': 'You\'re Welcome! 😊',
            'content': """
            Happy to help! Let me know if you have any other questions about:
            • Segment sources and destinations
            • mParticle user profiles
            • Lytics audience segments
            """
        }

    def _goodbye_response(self) -> Dict:
        return {
            'title': 'Goodbye! 👋',
            'content': """
            Thanks for chatting! Feel free to come back if you have more questions about CDPs.
            Have a great day!
            """
        }

    def _help_response(self) -> Dict:
        return {
            'title': 'How Can I Help? 🤝',
            'content': """
            I can help you with various CDP tasks:

            1. Segment:
            • Setting up data sources
            • Configuring destinations
            • Managing tracking

            2. mParticle:
            • Creating user profiles
            • Identity management
            • Data mapping

            3. Lytics:
            • Building audiences
            • Segmentation rules
            • Campaign activation

            Just ask me specific questions about any of these topics!
            """
        }

    def _capabilities_response(self) -> Dict:
        return {
            'title': 'My Capabilities 💡',
            'content': """
            I'm a specialized CDP assistant that can help you with:

            1. Step-by-step guides for:
            • Segment implementation
            • mParticle setup
            • Lytics configuration

            2. Best practices for:
            • Data collection
            • User identification
            • Audience building

            3. Technical documentation for:
            • API integrations
            • SDK implementations
            • Data mapping

            Try asking specific questions about these topics!
            """
        }

    def _cdp_overview_response(self) -> Dict:
        return {
            'title': 'Customer Data Platform (CDP) Overview',
            'content': """
            A CDP helps you collect, unify, and activate customer data:

            Key Features:
            • Data Collection (Sources)
            • Identity Resolution
            • Audience Segmentation
            • Data Activation (Destinations)

            I can help you with:
            1. Segment - Leading CDP for data collection
            2. mParticle - Mobile-first CDP
            3. Lytics - AI-driven CDP

            What specific aspect would you like to learn about?
            """
        } 