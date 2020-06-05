// Copyright (C) 2019 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#include <vector>

#include "common_test_utils/test_constants.hpp"
#include "single_layer_tests/reshape.hpp"

using LayerTestsDefinitions::ReshapeLayerTest;

namespace {
const std::vector<InferenceEngine::Precision> netPrecisions = {InferenceEngine::Precision::FP32,
                                                               InferenceEngine::Precision::FP16};

INSTANTIATE_TEST_CASE_P(ReshapeCheckDynBatch, ReshapeLayerTest,
                        ::testing::Combine(::testing::Values(true),                                   //
                                           ::testing::ValuesIn(netPrecisions),                        //
                                           ::testing::Values(std::vector<size_t>({30, 30, 30, 30})),  //
                                           ::testing::Values(std::vector<size_t>({30, 30, 30, 30})),  //
                                           ::testing::Values(CommonTestUtils::DEVICE_PLAIDML)),       //
                        ReshapeLayerTest::getTestCaseName);

INSTANTIATE_TEST_CASE_P(ReshapeCheck, ReshapeLayerTest,
                        ::testing::Combine(::testing::Values(true),                                   //
                                           ::testing::ValuesIn(netPrecisions),                        //
                                           ::testing::Values(std::vector<size_t>({10, 10, 10, 10})),  //
                                           ::testing::Values(std::vector<size_t>({10, 0, 100})),      //
                                           ::testing::Values(CommonTestUtils::DEVICE_PLAIDML)),       //
                        ReshapeLayerTest::getTestCaseName);
}  // namespace
