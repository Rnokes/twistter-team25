import React from "react";
import NavigationBar from "../../components/NavigationBar";
import PageTitle from "../../components/common/PageTitle";
import { blogDivStyle } from "../..";
import { Button, Container, Row, Col } from "react-bootstrap";
import BlogPosts from "../../views/BlogPosts";

export default class Topic_Animals extends React.Component {
  render() {
    return (
      <div className="MiscTopic" style={blogDivStyle}>
        <NavigationBar />
        <Container>
          <Row>
            <Col sm={8}>
              <PageTitle
                sm="4"
                title="Blog Posts"
                subtitle="Animals"
                className="text-sm-left"
              />
            </Col>
            <Col sm={4}>
              <Button type="submit" variant="dark">
                Follow Topic
              </Button>
            </Col>
          </Row>
        </Container>
        <BlogPosts topic="animals" />
      </div>
    );
  }
}
